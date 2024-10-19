**EXPLORING TIME DISTANCE TRADEOFFS IN MULTI-ROBOT TASK ALLOCATION USING MULTIOBJECTIVE GENETIC ALGORITHMS**

Final year project that explored solutions to multi objective multi robot task allocation using genetic algorithms. 
Initially explored a simple GA written in Python and DEAP library that optimises for distance and time seperately using fitness functions F1 and F2.
Then explored results to justify and develop naive multiobjective function F3 that optimises both goals. Eventually, we developed a more complex solution utilising NSGA-II algorithm.

![image](https://github.com/user-attachments/assets/9dde0e34-82c4-40b3-8ce4-f65a41947269)
UPDATES:
- Implemented 3D simulation over the original 2D view with animated visuals of robotic paths using Malplotlib Axes3C and FuncAnimation tools:

GIF

Then after comparing F1 and F2 solutions I found that their results varied significantly in failing to optimising for vice versa. 
Forexample when optimising for just distance not all the robots are allocated tasks to preserve battery but then we are not solving tasks concurrently and thus taking longer.

![image](https://github.com/user-attachments/assets/d42657c8-3bf5-4eb5-90ef-c184305870dc)

Simiarly, when solving for only time robots are exploring too far in order to ge tthe job done as quick as possible but pays no regard for preserving battery/distance.

![image](https://github.com/user-attachments/assets/bdafe643-92d9-4bea-bb39-ec2a0b23c78b)

After statistical analysis concluded that a significant conflict exists when optimising for time and distance.

![image](https://github.com/user-attachments/assets/c45b7bde-8938-4f7c-aa2e-751bb6890089)

Led to the development of a simple weighted fitness function F3 that equally optimised for both time and distance.
I successfully obtained statistically significant and better solutions that optimised for both time and distance that outperformed F1 and F2.

![image](https://github.com/user-attachments/assets/0d173de6-78af-4680-81c1-0fbeb8fb634f)

![image](https://github.com/user-attachments/assets/cb6d7865-d107-4d2b-b667-21dc609faccc)

While, this led to more balanced solutions although the diversity of the solutions were lacking as not all of these solutions were equally good.

![image](https://github.com/user-attachments/assets/e33351e8-cf7b-45c9-b683-4e4f23207e77)

Hence to improve and push my solutions further I developed a pure multiobjective solution utilising NSGA II algorithm.
This was done to obtain a pareto front of solutions that were equally good.

![image](https://github.com/user-attachments/assets/5a2aaff7-ebc5-4aa3-a28c-a11275106295)
![image](https://github.com/user-attachments/assets/87fdfeef-31b7-49b0-b987-2c461bcd1a31)

The NSGA 2 solution obtained task allocations that generally performed much better than F3 as most of its solutions minimised time and distance much more that F3 solutions.
Still there is room for improvement as one or two  F3 solutions were similar to NSGA II solutions which could also be limitations of my environment.

Additionally, the hyperparameters for F3 were optimised as part of the experiments:

![image](https://github.com/user-attachments/assets/43357187-a9f0-4e99-832c-96bc50fd639e)

Further work includes adding more tasks and robots and positional variations. 
Current work is static task allocation and work can be done to provide a more dynamic scenario by implementing simulations in MATLAB / Webots.
