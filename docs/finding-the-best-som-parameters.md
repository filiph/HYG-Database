

Variance

We want as small a variance as possible:

Old variance model ((a_b_distance_3d/b_c_distance_3d) - (a_b_distance_2d/b_c_distance_2d))

create_som.organize(stars[:100], width=100, height=100, iters=1000, learning_rate=0.2)  # 1900
create_som.organize(stars[:100], width=100, height=100, iters=100, learning_rate=0.2)  # 1618
create_som.organize(stars[:100], width=100, height=100, iters=100, learning_rate=0.1)  # 2007
create_som.organize(stars[:100], width=100, height=100, iters=1000, learning_rate=0.1)  # 2014

New variance model ((a_b_distance_3d/a_b_distance_2d) - (b_c_distance_3d/b_c_distance_2d))

create_som.organize(stars[:100], width=100, height=100, iters=1000, learning_rate=0.1)  # 2023
create_som.organize(stars[:100], width=100, height=100, iters=1, learning_rate=0.1)  # 1376  WTF?
create_som.organize(stars[:100], width=100, height=100, iters=1, learning_rate=0.01)  # 1600
create_som.organize(stars[:100], width=100, height=100, iters=1, learning_rate=0.2)  # 1554
create_som.organize(stars[:100], width=100, height=100, iters=100, learning_rate=0.2)  # 1657

Back to old variance model ((a_b_distance_3d/b_c_distance_3d) - (a_b_distance_2d/b_c_distance_2d)) with newer variance computation

create_som.organize(stars[:100], width=100, height=100, iters=100, learning_rate=0.2)  # 1661
create_som.organize(stars[:100], width=100, height=100, iters=1, learning_rate=0.2)  # 1637
create_som.organize(stars[:100], width=100, height=100, iters=10, learning_rate=0.2)  # 2155
create_som.organize(stars[:100], width=100, height=100, iters=10, learning_rate=0.05)  # 1737
create_som.organize(stars[:100], width=100, height=100, iters=100, learning_rate=0.05)  # 2192
create_som.organize(stars[:100], width=100, height=100, iters=100, learning_rate=0.005)  # 1971


Back to old variance model ((a_b_distance_3d/b_c_distance_3d) - (a_b_distance_2d/b_c_distance_2d)) with percentage below diff of 0.5

create_som.organize(stars[:100], width=100, height=100, iters=100, learning_rate=0.005)  # 70%
create_som.organize(stars[:100], width=100, height=100, iters=1, learning_rate=0.005)  # 45%
create_som.organize(stars[:100], width=100, height=100, iters=200, learning_rate=0.005)  # 65%
create_som.organize(stars[:100], width=100, height=100, iters=200, learning_rate=0.05)  # 53%
create_som.organize(stars[:100], width=100, height=100, iters=200, learning_rate=0.5)  # 99% -- all on the same place!!!
create_som.organize(stars[:100], width=100, height=100, iters=100, learning_rate=0.1)  # 57%
create_som.organize(stars[:100], width=100, height=100, iters=100, learning_rate=0.001)  # 98% ???
create_som.organize(stars[:100], width=100, height=100, iters=1000, learning_rate=0.001)  # 71%
create_som.organize(stars[:100], width=100, height=100, iters=100, learning_rate=0.001)  # again -> 94%, but also lots of zeroes