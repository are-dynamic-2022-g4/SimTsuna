pub const fn dir_to_index(x: i8, y: i8, z: i8) -> usize {
    (x + 1 + (y + 1) * 3 + (z + 1) * 9) as usize
}

pub const WEIGHTS: [f32; 27] = {
    let mut weights = [0.0; 27];
    let mut x = -1;
    while x < 2 {
        let mut y = -1;
        while y < 2 {
            let mut z = -1;
            while z < 2 {
                let index = dir_to_index(x, y, z);
                let dir_sum = x.abs() + y.abs() + z.abs();
                let weight = match dir_sum {
                    0 => 8.0 / 27.0,
                    1 => 2.0 / 27.0,
                    2 => 1.0 / 54.0,
                    3 => 1.0 / 216.0,
                    _ => 0.0 // unreachable
                };
                weights[index] = weight;
                z += 1;
            }
            y += 1;
        }
        x += 1;
    }
    weights
};

#[derive(Debug, Copy, Clone)]
pub struct FluidTile {
    pub vels: [f32; 27]
}

impl FluidTile {
    pub fn empty() -> Self {
        Self {
            vels: [0.0; 27]
        }
    }

    pub fn rho_u(&self) -> (f32, f32, f32) {
        let mut u_x = 0.0;
        let mut u_y = 0.0;
        let mut u_z = 0.0;

        for x in -1..=1 {
            for y in -1..=1 {
                for z in -1..=1 {
                    let idx = dir_to_index(x, y, z);
                    let n = self.vels[idx];
                    u_x += n * x as f32;
                    u_y += n * y as f32;
                    u_z += n * z as f32;
                }
            }
        }

        (u_x, u_y, u_z)
    }

    pub fn rho(&self) -> f32 {
        let mut r = 0.0;
        for i in &self.vels {
            r += *i;
        }
        r
    }
}