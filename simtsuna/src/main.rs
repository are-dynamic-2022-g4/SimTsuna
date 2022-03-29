use nannou::prelude::*;
use simtsuna::engine::{Engine, SIZE_X, SIZE_Y, SIZE_Z};
use simtsuna::engine::fluid_tile::{dir_to_index, WEIGHTS};

const PX_SIZE_X: f32 = 5.0;
const PX_SIZE_Y: f32 = 5.0;

enum EngineCameraAxis {
    X,
    Y,
    Z
}

enum EngineCameraMode {
    Density,
    VelocityAll,
    VelocityX,
    VelocityY,
    VelocityZ
}

struct EngineCamera {
    axis: EngineCameraAxis,
    mode: EngineCameraMode,
    layer: usize
}

struct Model {
    engine: Engine,
    engine_camera: EngineCamera,
    time_since_last_step: f32,
    seconds_per_step: f32,
    current_step: usize,
    last_mouse_x: f32,
    last_mouse_y: f32,
}

fn main() {
    nannou::app(model)
        .update(update)
        .simple_window(view)
        .run();
}

fn model(_: &App) -> Model {
    Model {
        engine: Engine::new(),
        engine_camera: EngineCamera {
            axis: EngineCameraAxis::Z,
            mode: EngineCameraMode::Density,
            layer: 0
        },
        time_since_last_step: 0.0,
        seconds_per_step: 0.10,
        current_step: 0,
        last_mouse_x: 0.0,
        last_mouse_y: 0.0
    }
}

fn update(app: &App, model: &mut Model, update: Update) {
    let mouse_x = app.mouse.x;
    let mouse_y = app.mouse.y;

    model.time_since_last_step += update.since_last.as_secs_f32();
    while model.time_since_last_step >= model.seconds_per_step {
        model.engine.step();
        model.current_step += 1;
        model.time_since_last_step -= model.seconds_per_step;
    }

    if app.mouse.buttons.left().is_down() {
        let x = mouse_x / PX_SIZE_X;
        let y = mouse_y / PX_SIZE_Y;

        if x < 0.0 || y < 0.0 { return; }
        let x = x as usize;
        let y = y as usize;
        if x >= SIZE_X || y >= SIZE_Y { return; }

        model.engine.fluid_grid[x][y][0].vels[dir_to_index(0, 0, 0)] += 100.0;
    }

    if app.mouse.buttons.right().is_down() {
        let x = mouse_x / PX_SIZE_X;
        let y = mouse_y / PX_SIZE_Y;

        if x < 0.0 || y < 0.0 { return; }
        let x = x as usize;
        let y = y as usize;
        if x >= SIZE_X || y >= SIZE_Y { return; }

        let diff_x = mouse_x - model.last_mouse_x;
        let diff_y = mouse_y - model.last_mouse_y;
        if diff_x > 0.0 {
            model.engine.fluid_grid[x][y][0].vels[dir_to_index(1, 0, 0)] += diff_x;
        }
        else {
            model.engine.fluid_grid[x][y][0].vels[dir_to_index(-1, 0, 0)] -= diff_x;
        }
        if diff_y > 0.0 {
            model.engine.fluid_grid[x][y][0].vels[dir_to_index(0, 1, 0)] += diff_y;
        }
        else {
            model.engine.fluid_grid[x][y][0].vels[dir_to_index(0, -1, 0)] -= diff_y;
        }
    }

    model.last_mouse_x = mouse_x;
    model.last_mouse_y = mouse_y;
}

fn view(app: &App, model: &Model, frame: Frame) {
    let draw = app.draw();
    draw.background().color(BLACK);

    let layer_size = match model.engine_camera.axis {
        EngineCameraAxis::X => (SIZE_Y, SIZE_Z),
        EngineCameraAxis::Y => (SIZE_X, SIZE_Z),
        EngineCameraAxis::Z => (SIZE_X, SIZE_Y)
    };

    let average_rho = model.engine.average_rho();

    for layer_x in 0..layer_size.0 {
        for layer_y in 0..layer_size.1 {
            let (x, y, z) = match model.engine_camera.axis {
                EngineCameraAxis::X => (model.engine_camera.layer, layer_x, layer_y),
                EngineCameraAxis::Y => (layer_x, model.engine_camera.layer, layer_y),
                EngineCameraAxis::Z => (layer_x, layer_y, model.engine_camera.layer)
            };
            let tile = &model.engine.fluid_grid[x][y][z];
            draw.rect()
                .color(match model.engine_camera.mode {
                    EngineCameraMode::Density => {
                        let rho = tile.rho();
                        let c = rho / average_rho / 3.0;
                        rgb(c, c, c)
                    }
                    EngineCameraMode::VelocityAll => {
                        let rho = tile.rho();
                        let rho_u = tile.rho_u();
                        rgb((rho_u.0 / rho + 1.0) / 2.0, (rho_u.1 / rho + 1.0) / 2.0, (rho_u.2 / rho + 1.0) / 2.0)
                    }
                    EngineCameraMode::VelocityX => {
                        let rho = tile.rho();
                        let rho_u = tile.rho_u();
                        let c = rho_u.0 / rho;
                        if c < 0.0 {
                            rgb(c, 0.0, 0.0)
                        }
                        else {
                            rgb(0.0, c, 0.0)
                        }
                    }
                    EngineCameraMode::VelocityY => {
                        let rho = tile.rho();
                        let rho_u = tile.rho_u();
                        let c = rho_u.1 / rho;
                        if c < 0.0 {
                            rgb(c, 0.0, 0.0)
                        }
                        else {
                            rgb(0.0, c, 0.0)
                        }
                    }
                    EngineCameraMode::VelocityZ => {
                        let rho = tile.rho();
                        let rho_u = tile.rho_u();
                        let c = rho_u.2 / rho + 1.0;
                        if c < 0.0 {
                            rgb(c, 0.0, 0.0)
                        }
                        else {
                            rgb(0.0, c, 0.0)
                        }
                    }
                })
                .x(layer_x as f32 * PX_SIZE_X)
                .y(layer_y as f32 * PX_SIZE_Y)
                .w(PX_SIZE_X)
                .h(PX_SIZE_Y);
        }
    }

    draw.text(&format!("Step {} : ", model.current_step))
        .x(-50.0)
        .y(-50.0);

    draw.to_frame(app, &frame).unwrap();
}
