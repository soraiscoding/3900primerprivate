# Document your edge case here
- To get marks for this section you will need to explain to your tutor:
1) The edge case you identified

If all students don't have a mark when we call get_stats.

2) How you have accounted for this in your implementation

Initialised all the stats that will be returned from the get_stats route so that we hopefully don't get an error when returning an object with the stats.

average is 0 since it would be 0 if nobody has any marks or if there were no students.

When looping through and checking the marks for all students I also checked if the mark exists or not.