import voluptuous as vol

from esphomeyaml.components import sensor
import esphomeyaml.config_validation as cv
from esphomeyaml.const import CONF_ID, CONF_LAMBDA, CONF_SENSORS, CONF_NAME
from esphomeyaml.cpp_generator import process_lambda, variable, Pvariable, add
from esphomeyaml.cpp_types import std_vector

CustomSensorConstructor = sensor.sensor_ns.class_('CustomSensorConstructor')

PLATFORM_SCHEMA = sensor.PLATFORM_SCHEMA.extend({
    cv.GenerateID(): cv.declare_variable_id(CustomSensorConstructor),
    vol.Required(CONF_LAMBDA): cv.lambda_,
    vol.Required(CONF_SENSORS): cv.ensure_list(sensor.SENSOR_SCHEMA.extend({
        cv.GenerateID(): cv.declare_variable_id(sensor.Sensor),
    })),
})


def to_code(config):
    for template_ in process_lambda(config[CONF_LAMBDA], [],
                                    return_type=std_vector.template(sensor.SensorPtr)):
        yield

    rhs = CustomSensorConstructor(template_)
    custom = variable(config[CONF_ID], rhs)
    for i, conf in enumerate(config[CONF_SENSORS]):
        var = Pvariable(conf[CONF_ID], custom.get_sensor(i))
        add(var.set_name(conf[CONF_NAME]))
        sensor.setup_sensor(var, conf)


BUILD_FLAGS = '-DUSE_CUSTOM_SENSOR'


def to_hass_config(data, config):
    return [sensor.core_to_hass_config(data, sens) for sens in config[CONF_SENSORS]]
