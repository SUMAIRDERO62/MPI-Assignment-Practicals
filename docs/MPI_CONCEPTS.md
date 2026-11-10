# MPI concepts at a glance

| Concept | Meaning | Practical |
|---|---|---|
| Rank and size | Process identity and communicator size | 01 |
| Send / receive | Explicit message between two ranks | 02 |
| Scatterv | Root sends uneven chunks | 03, 04 |
| Gatherv | Root gathers uneven chunks | 03, 05, 06 |
| Broadcast | Root shares one value with all ranks | 06 |
| Reduce | Combines values at one root | 04 |
| Barrier | Synchronizes ranks before a timed phase | Existing benchmark |

Point-to-point operations target specific ranks. Collective operations involve
every rank in the communicator and must be called consistently by all
participants. Scatter distributes pieces of one buffer; broadcast sends the
same value to everyone. Gather collects pieces, while reduce combines values
using an operation such as `MPI.SUM`.

The dashboard visualizer illustrates these flows in the browser, but its output
is explicitly a simulation and not a measurement of MPI.
