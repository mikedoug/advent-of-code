using System;
using System.Diagnostics;

namespace TimeIt {
    public class TimeIt : IDisposable
    {
        private Stopwatch timer = new Stopwatch();
        private string description;

        public TimeIt(string description) {
            timer.Start();
            this.description = description;
        }

        public void Dispose()
        {
            timer.Stop();
            Console.WriteLine($"{description}: {timer.Elapsed}");
        }
    }
}