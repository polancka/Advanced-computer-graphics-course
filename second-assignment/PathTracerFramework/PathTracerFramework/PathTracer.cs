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
            var L = Spectrum.Create(0);
            if (s == null) { 
                Debug.WriteLine("No scene");
                return null;
            }
            else
            {
                int maxDepth = 10;
                L = Spectrum.Create(0);
                var beta = 1;
                //var nbounces = 0;

                for (int i = 0; i < maxDepth; i++)
                {
                    var intersect = s.Intersect(r);
                    if (intersect.Item1 == null) {
                        break;
                    }
                    //Debug.WriteLine(intersect.Item2.Obj.ToString());
                    //var wo = -r;
                    //TODO: Check if the light is hit
                    //if(intersect.Item2.Obj == Light)
                    //{
                    //    //light was hit, find light emitted
                    //    L = beta * intersect.Item2.Wo;
                    //    break;
                    //}
                    //sample random reflection
                    var wi = Ray.Generate(intersect.Item2.Point, Vector3.ZeroVector);
                    //update beta
                    //(f,pr) <- bsdf(intersectm wi, wo)
                    //beta = beta * f * |cosfi|/pr
                    //r = wi
                    //nbounces++
                  
                L.AddTo(Spectrum.Create(0.1));
                }
                //add L to image  AddSampleToImage(L,r)
                //L = Spectrum.Create(random.Next(0,1));

            }
            return L;
        }

    }
}
