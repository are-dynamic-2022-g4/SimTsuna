use std::mem::MaybeUninit;
use std::process::exit;
use nannou::color::white_point::B;
use nannou::prelude::{Pow, Zero};
use crate::engine::fluid_tile::{dir_to_index, FluidTile, WEIGHTS};

pub mod fluid_tile;

pub const SIZE_X: usize = 50;
pub const SIZE_Y: usize = 50;
pub const SIZE_Z: usize = 30;

pub struct Engine {
    pub fluid_grid: Box<[[[FluidTile; SIZE_Z]; SIZE_Y]; SIZE_X]>,
    pub tau: f32
}

impl Engine {
    pub fn new() -> Self {
        let mut fluid_grid = Box::new([[[MaybeUninit::uninit(); SIZE_Z]; SIZE_Y]; SIZE_X]);

        for x in 0..SIZE_X {
            for y in 0..SIZE_Y {
                for z in 0..SIZE_Z {
                    fluid_grid[x][y][z] = MaybeUninit::new(FluidTile {
                        vels: [1.0; WEIGHTS.len()]
                    });
                }
            }
        }

        let mut result = Self {
            fluid_grid: unsafe { std::mem::transmute(fluid_grid) },
            tau: 1.0
        };

        result
    }

    fn drift(&mut self) {
        impl Engine {
            fn roll_x(&mut self, vel: usize) {
                for y in 0..SIZE_Y {
                    for z in 0..SIZE_Z {
                        let first = self.fluid_grid[0][y][z].vels[vel];
                        for x in 0..(SIZE_X - 1) {
                            self.fluid_grid[x][y][z].vels[vel] = self.fluid_grid[x + 1][y][z].vels[vel];
                        }
                        self.fluid_grid[SIZE_X - 1][y][z].vels[vel] = first;
                    }
                }
            }

            fn roll_y(&mut self, vel: usize) {
                for x in 0..SIZE_X {
                    for z in 0..SIZE_Z {
                        let first = self.fluid_grid[x][0][z].vels[vel];
                        for y in 0..(SIZE_Y - 1) {
                            self.fluid_grid[x][y][z].vels[vel] = self.fluid_grid[x][y + 1][z].vels[vel];
                        }
                        self.fluid_grid[x][SIZE_Y - 1][z].vels[vel] = first;
                    }
                }
            }

            fn roll_z(&mut self, vel: usize) {
                for x in 0..SIZE_X {
                    for y in 0..SIZE_Y {
                        let first = self.fluid_grid[x][y][0].vels[vel];
                        for z in 0..(SIZE_Z - 1) {
                            self.fluid_grid[x][y][z].vels[vel] = self.fluid_grid[x][y][z + 1].vels[vel];
                        }
                        self.fluid_grid[x][y][SIZE_Z - 1].vels[vel] = first;
                    }
                }
            }

            fn roll_nx(&mut self, vel: usize) {
                for y in 0..SIZE_Y {
                    for z in 0..SIZE_Z {
                        let last = self.fluid_grid[SIZE_X - 1][y][z].vels[vel];
                        for x in (1..SIZE_X).rev() {
                            self.fluid_grid[x][y][z].vels[vel] = self.fluid_grid[x - 1][y][z].vels[vel];
                        }
                        self.fluid_grid[0][y][z].vels[vel] = last;
                    }
                }
            }

            fn roll_ny(&mut self, vel: usize) {
                for x in 0..SIZE_X {
                    for z in 0..SIZE_Z {
                        let last = self.fluid_grid[x][SIZE_Y - 1][z].vels[vel];
                        for y in (1..SIZE_Y).rev() {
                            self.fluid_grid[x][y][z].vels[vel] = self.fluid_grid[x][y - 1][z].vels[vel];
                        }
                        self.fluid_grid[x][0][z].vels[vel] = last;
                    }
                }
            }

            fn roll_nz(&mut self, vel: usize) {
                for x in 0..SIZE_X {
                    for y in 0..SIZE_Y {
                        let last = self.fluid_grid[x][y][SIZE_Z - 1].vels[vel];
                        for z in (1..SIZE_Z).rev() {
                            self.fluid_grid[x][y][z].vels[vel] = self.fluid_grid[x][y][z - 1].vels[vel];
                        }
                        self.fluid_grid[x][y][0].vels[vel] = last;
                    }
                }
            }
        }

        for x in -1..=1 {
            for y in -1..=1 {
                for z in -1..=1 {
                    let idx = dir_to_index(x, y, z);
                    if x == -1 { self.roll_x(idx); }
                    if x == 1 { self.roll_nx(idx); }
                    if y == -1 { self.roll_y(idx); }
                    if y == 1 { self.roll_ny(idx); }
                    if z == -1 { self.roll_z(idx); }
                    if z == 1 { self.roll_nz(idx); }
                }
            }
        }
    }

    pub fn collide(&mut self) {
        fn dot(a: (f32, f32, f32), b: (f32, f32, f32)) -> f32 {
            a.0 * b.0 + a.1 * b.1 + a.2 * b.2
        }

        let tau = self.tau;

        for x in 0..SIZE_X {
            for y in 0..SIZE_Y {
                for z in 0..SIZE_Z {
                    let rho = self.fluid_grid[x][y][z].rho();

                    let rho_u = self.fluid_grid[x][y][z].rho_u();
                    let u = (rho_u.0 / rho, rho_u.1 / rho, rho_u.2 / rho);

                    for vel_x in -1..=1 {
                        for vel_y in -1..=1 {
                            for vel_z in -1..=1 {
                                let idx = dir_to_index(vel_x, vel_y, vel_z);

                                let e = (vel_x as f32, vel_y as f32, vel_z as f32);
                                let sum =
                                    1.0
                                    + (3.0 * dot(e, u))
                                    + ((9.0 / 2.0) * dot(e, u).pow(2) as f32)
                                    - ((3.0 / 2.0) * dot(u, u));
                                let eq = rho * WEIGHTS[idx] * sum;

                                self.fluid_grid[x][y][z].vels[idx] -=
                                    (1.0 / tau) * (self.fluid_grid[x][y][z].vels[idx] - eq);
                            }
                        }
                    }
                }
            }
        }
    }

    pub fn step(&mut self) {
        self.drift();
        self.collide();
    }

    pub fn total_rho(&self) -> f32 {
        let mut t = 0.0;
        for x in 0..SIZE_X {
            for y in 0..SIZE_Y {
                for z in 0..SIZE_Z {
                    t += self.fluid_grid[x][y][z].rho();
                }
            }
        }
        t
    }

    pub fn average_rho(&self) -> f32 {
        self.total_rho() / (SIZE_X * SIZE_Y * SIZE_Z) as f32
    }
}