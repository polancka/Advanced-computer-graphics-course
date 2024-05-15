using System;
using MathNet.Numerics.Integration;

namespace PathTracer
{
    /// <summary>
    /// Sphere Shape template class - NOT implemented completely
    /// </summary>
    class Sphere : Shape
    {
        public double Radius { get; set; }
        public Sphere(double radius, Transform objectToWorld)
        {
            Radius = radius;
            ObjectToWorld = objectToWorld;
        }

        /// <summary>
        /// Ray-Sphere intersection - NOT implemented
        /// </summary>
        /// <param name="r">Ray</param>
        /// <returns>t or null if no hit, point on surface</returns>
        public override (double?, SurfaceInteraction) Intersect(Ray ray)
        {
            Ray r = WorldToObject.Apply(ray);

            double ox = r.o.x;
            double oy = r.o.y;
            double oz = r.o.z;
            double dx = r.d.x;
            double dy = r.d.y; 
            double dz = r.d.z;
           
            double a = dx * dx + dy * dy + dz * dz;
            double b = 2 * (dx * ox + dy * oy + dz * oz);
            double c = ox * ox + oy * oy + oz * oz - Radius * Radius;


            (bool isSolution, double t0, double t1) = Utils.Quadratic(a, b, c);
            if (!isSolution)
            {
                return (null, null);
            }

            if (t1 <= 0) return (null, null);
            double tShapeHit = t0;
            if (tShapeHit <= 0)
            {
                tShapeHit = t1;
            }

            Vector3 pHit = r.Point(tShapeHit);
            pHit *= Radius / pHit.Length();

            Vector3 normal = pHit.Clone().Normalize();
            Vector3 minus_pHit = -pHit;
            Vector3 dpdu = new Vector3(minus_pHit.y, pHit.x, 0);
       
            SurfaceInteraction interection = new SurfaceInteraction(pHit, normal, -r.d, dpdu, this);

            // A dummy return example
            //double dummyHit = 0.0;
            //Vector3 dummyVector = new Vector3(0, 0, 0);
            //SurfaceInteraction dummySurfaceInteraction = new SurfaceInteraction(dummyVector, dummyVector, dummyVector, dummyVector, this);
            //return (dummyHit, dummySurfaceInteraction);
            return (tShapeHit, ObjectToWorld.Apply(interection));
        }

        /// <summary>
        /// Sample point on sphere in world
        /// </summary>
        /// <returns>point in world, pdf of point</returns>
        public override (SurfaceInteraction, double) Sample()
        {
            // TODO: Implement Sphere sampling
            Vector3 pObj = new Vector3(0, 0, 0) + Radius * Samplers.UniformSampleSphere();

            // TODO: Return surface interaction and pdf

            // A dummy return example
            //double dummyPdf = 1.0;
            //Vector3 dummyVector = new Vector3(0, 0, 0);
            //SurfaceInteraction dummySurfaceInteraction = new SurfaceInteraction(dummyVector, dummyVector, dummyVector, dummyVector, this);
            //return (dummySurfaceInteraction, dummyPdf);
            Vector3 n = ObjectToWorld.ApplyNormal(pObj);

            bool reverseOrientation = false;
            if (reverseOrientation)
            {
                n *= -1;
            }
            pObj *= Radius / pObj.Length();
            Vector3 dpdu = new Vector3(-pObj.y, pObj.x, 0);
            double pdf = 1 / Area();

            return (ObjectToWorld.Apply(new SurfaceInteraction(pObj, n, Vector3.ZeroVector, dpdu, this)), pdf);
        }

        public override double Area() { return 4 * Math.PI * Radius * Radius; }

        /// <summary>
        /// Estimates pdf of wi starting from point si
        /// </summary>
        /// <param name="si">point on surface that wi starts from</param>
        /// <param name="wi">wi</param>
        /// <returns>pdf of wi given this shape</returns>
        public override double Pdf(SurfaceInteraction si, Vector3 wi)
        {
            return 1 / Area(); ;
        }

    }
}
