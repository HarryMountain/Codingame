import cProfile
from CodeVsZombies.test_code_vs_zombies import TestCodeVsZombies
cProfile.run("TestCodeVsZombies().test_mass_zombie_attack()")
