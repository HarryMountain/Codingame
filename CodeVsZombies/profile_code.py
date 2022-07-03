import cProfile
from CodeVsZombies.test_code_vs_zombies import TestCodeVsZombies
#cProfile.run("TestCodeVsZombies().test_mass_zombie_attack()")
cProfile.run("TestCodeVsZombies().test_case1_single_zombie_single_human()")
