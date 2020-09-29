#pragma once

#include "esphome/core/component.h"
#include "esphome/components/gpio/switch/gpio_switch.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/mqtt/custom_mqtt_device.h"

static const char *TAG = "dosage_switch";

namespace esphome {
namespace dosage {

class DosageSwitch : public gpio::GPIOSwitch, public mqtt::CustomMQTTDevice {
 public:
  void dose_for_ms(uint32_t time_in_ms) ;
  void dose_for_seconds(uint32_t time_in_seconds) ;
  void dose();
  void dose(float times);

  void on_dose_for_ms(const std::string &topic, const std::string &payload) { this->dose_for_ms(uint32_t(atoi(payload.c_str()))); }
  void on_dose_for_seconds(const std::string &topic, const std::string &payload) { this->dose_for_seconds(uint32_t(atoi(payload.c_str()))); }
  void on_set_dosage(const std::string &topic, const std::string &payload) { 
    this->set_dosage(uint32_t(atoi(payload.c_str()))); 
  }
  void on_dose(const std::string &topic, const std::string &payload) { this->dose(); }

  void setup() override;
  void dump_config() override;
  std::string component_type() const { return "switch"; }
  std::string get_default_object_id() const { return sanitize_string_allowlist(to_lowercase_underscore(this->get_name()), HOSTNAME_CHARACTER_ALLOWLIST); }
  void set_dosage(uint32_t dosage) { 
    ESP_LOGD(TAG,"Updating dosage to be %d ms",dosage);
    dosage_->publish_state(dosage); 
  }
  void set_sensor(sensor::Sensor *sensor) { dosage_ = sensor; }
  void set_exact_timing(bool exact_timing) { exact_timing_ = exact_timing; }

  void set_topic_dose(std::string topic_dose ) { this->topic_dose = topic_dose; }
  void set_topic_set_dosage(std::string topic_set_dosage ) { this->topic_set_dosage = topic_set_dosage; }
  void set_topic_dose_for_ms(std::string topic_dose_for_ms ) { this->topic_dose_for_ms = topic_dose_for_ms; }
  void set_topic_dose_for_seconds(std::string topic_dose_for_seconds ) { this->topic_dose_for_seconds = topic_dose_for_seconds; }

  void cancel_dose();
  uint32_t get_dosage() { return this->dosage_->state; }

 protected:
  sensor::Sensor *dosage_{nullptr};
  bool exact_timing_;
  std::string topic_dose_for_seconds;
  std::string topic_dose_for_ms;
  std::string topic_set_dosage;
  std::string topic_dose;
};

}  // namespace dosage
}  // namespace esphome
