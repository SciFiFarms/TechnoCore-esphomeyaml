import voluptuous as vol

from esphomeyaml.components import binary_sensor
import esphomeyaml.config_validation as cv
from esphomeyaml.const import CONF_BINARY_SENSORS, CONF_ID, CONF_LAMBDA, CONF_NAME
from esphomeyaml.cpp_generator import process_lambda, variable, Pvariable, add
from esphomeyaml.cpp_types import std_vector

CustomBinarySensorConstructor = binary_sensor.binary_sensor_ns.class_(
    'CustomBinarySensorConstructor')

PLATFORM_SCHEMA = binary_sensor.PLATFORM_SCHEMA.extend({
    cv.GenerateID(): cv.declare_variable_id(CustomBinarySensorConstructor),
    vol.Required(CONF_LAMBDA): cv.lambda_,
    vol.Required(CONF_BINARY_SENSORS):
        cv.ensure_list(binary_sensor.BINARY_SENSOR_SCHEMA.extend({
            cv.GenerateID(): cv.declare_variable_id(binary_sensor.BinarySensor),
        })),
})


def to_code(config):
    for template_ in process_lambda(config[CONF_LAMBDA], [],
                                    return_type=std_vector.template(binary_sensor.BinarySensorPtr)):
        yield

    rhs = CustomBinarySensorConstructor(template_)
    custom = variable(config[CONF_ID], rhs)
    for i, conf in enumerate(config[CONF_BINARY_SENSORS]):
        var = Pvariable(conf[CONF_ID], custom.get_binary_sensor(i))
        add(var.set_name(conf[CONF_NAME]))
        binary_sensor.setup_binary_sensor(var, conf)


BUILD_FLAGS = '-DUSE_CUSTOM_BINARY_SENSOR'


def to_hass_config(data, config):
    return [binary_sensor.core_to_hass_config(data, sens) for sens in config[CONF_BINARY_SENSORS]]
