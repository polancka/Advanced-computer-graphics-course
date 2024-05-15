using System;
using System.Diagnostics;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using static PathTracer.Samplers;

namespace PathTracer
{
    class PathTracer
    {
        private Random random;

        public PathTracer()
        {

            random = new Random();   
        }
        /// <summary>
        /// Given Ray r and Scene s, trace the ray over the scene and return the estimated radiance
        /// </summary>
        /// <param name="r">Ray direction</param>
        /// <param name="s">Scene to trace</param>
        /// <returns>Estimated radiance in the ray direction</returns>
        ///  
        public Spectrum Li(Ray r, Scene s)
        {
            Random random = new Random();
            var L = Spectrum.ZeroSpectrum;
            Spectrum beta = Spectrum.Create(1.0);

            if (s == null)
            {
                Debug.WriteLine("no scene");
                return null;
            }
            else
            {   
                int maxdepth = 30;

                for (int i = 0; i < maxdepth; i++)
                {
                    var intersect = s.Intersect(r);
                    (double? distance, SurfaceInteraction intersection) = intersect;
                    if (!distance.HasValue)
                    {
                        break;
                    }
                    
                    
                    //check if the light is hit
                    if(intersection.Obj is Light)
                    {   
                        if(i == 0)
                        {
                           //light was hit, find light emitted
                            L = L.AddTo(beta * intersection.Le(-r.d));

                        }
                        break;
                    }

                    //if light was not hit
                    L = L.AddTo(beta * Light.UniformSampleOneLight(intersection, s));
                    Shape obj = (Shape)intersection.Obj;

                    //sample random reflection
                    var new_info = obj.BSDF.Sample_f(-r.d, intersection);
                    (Spectrum f, Vector3 wi, double pdf, bool isSpecular) = new_info;
                    r = intersection.SpawnRay(wi);
                    //update beta
                    //(f,pr) <- bsdf(intersectm wi, wo)
                    //beta = beta * f * |cosfi|/pr
                    //r = wi
                    beta = beta * (f * Vector3.AbsDot(wi, intersection.Normal) / pdf);

                    //Russian roullete for termination after 5 reflections
                    if (i > 5)
                    {
                        double q = 1 - beta.c.Max();
                        if (random.NextDouble() < q)
                        {
                            break;
                        }
                        beta = beta / (1 - q);
                    }
                }
            }
            return L;
        }

    }
}
