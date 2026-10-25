//! ============================================================================
//! DAXOS CLOCK & WORLD TIME SUITE (dax-clock)
//! File: crates/dax-clock/src/lib.rs
//! Version: 1.10.2026 'Rhino' (ALPHA)
//! Architect: Dhafa Nazula Permadi (@kangpcode)
//! Modules: World Clock, Alarm, Stopwatch, Countdown Timer
//! Strictly ZERO EMOJIS
//! ============================================================================

use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WorldCity {
    pub name: String,
    pub country: String,
    pub utc_offset_hours: i32,
    pub timezone_code: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AlarmItem {
    pub id: u32,
    pub time_str: String, // "06:00"
    pub label: String,
    pub repeat_days: String, // "Senin - Jumat", "Setiap Hari"
    pub is_active: bool,
    pub chime_sound: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StopwatchLap {
    pub lap_number: usize,
    pub lap_time_ms: u64,
    pub total_time_ms: u64,
}

pub struct DaxClockEngine;

impl DaxClockEngine {
    pub fn get_world_cities() -> Vec<WorldCity> {
        vec![
            WorldCity {
                name: "Jakarta".to_string(),
                country: "Indonesia".to_string(),
                utc_offset_hours: 7,
                timezone_code: "WIB".to_string(),
            },
            WorldCity {
                name: "Tokyo".to_string(),
                country: "Jepang".to_string(),
                utc_offset_hours: 9,
                timezone_code: "JST".to_string(),
            },
            WorldCity {
                name: "London".to_string(),
                country: "Inggris Raya".to_string(),
                utc_offset_hours: 0,
                timezone_code: "GMT".to_string(),
            },
            WorldCity {
                name: "New York".to_string(),
                country: "Amerika Serikat".to_string(),
                utc_offset_hours: -5,
                timezone_code: "EST".to_string(),
            },
            WorldCity {
                name: "Sydney".to_string(),
                country: "Australia".to_string(),
                utc_offset_hours: 10,
                timezone_code: "AEST".to_string(),
            },
        ]
    }

    pub fn get_city_time(city: &WorldCity, now_utc: DateTime<Utc>) -> (String, String, bool) {
        // Calculate local hours
        let raw_hour = (now_utc.format("%H").to_string().parse::<i32>().unwrap_or(0) + city.utc_offset_hours + 24) % 24;
        let minute = now_utc.format("%M").to_string();
        let second = now_utc.format("%S").to_string();

        let time_str = format!("{:02}:{:02}:{:02}", raw_hour, minute, second);
        let diff_str = if city.utc_offset_hours >= 7 {
            format!("+{} jam dari Jakarta", city.utc_offset_hours - 7)
        } else {
            format!("{} jam dari Jakarta", city.utc_offset_hours - 7)
        };
        let is_day = raw_hour >= 6 && raw_hour < 18;

        (time_str, diff_str, is_day)
    }

    pub fn get_default_alarms() -> Vec<AlarmItem> {
        vec![
            AlarmItem {
                id: 1,
                time_str: "05:00".to_string(),
                label: "Subuh & Persiapan Kerja".to_string(),
                repeat_days: "Setiap Hari".to_string(),
                is_active: true,
                chime_sound: "Symphonic Dawn".to_string(),
            },
            AlarmItem {
                id: 2,
                time_str: "09:00".to_string(),
                label: "Daily Standup Sprint DAXOS".to_string(),
                repeat_days: "Senin - Jumat".to_string(),
                is_active: true,
                chime_sound: "Glass Chime".to_string(),
            },
            AlarmItem {
                id: 3,
                time_str: "14:00".to_string(),
                label: "Code Review & Architecture Sync".to_string(),
                repeat_days: "Senin - Jumat".to_string(),
                is_active: false,
                chime_sound: "Harp Resonance".to_string(),
            },
        ]
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_world_cities() {
        let cities = DaxClockEngine::get_world_cities();
        assert_eq!(cities.len(), 5);
        assert_eq!(cities[0].name, "Jakarta");
        assert_eq!(cities[0].utc_offset_hours, 7);
    }

    #[test]
    fn test_city_time_calculation() {
        let cities = DaxClockEngine::get_world_cities();
        let now = Utc::now();
        let (time_str, _diff, _) = DaxClockEngine::get_city_time(&cities[0], now);
        assert_eq!(time_str.len(), 8);
    }

    #[test]
    fn test_alarms_list() {
        let alarms = DaxClockEngine::get_default_alarms();
        assert_eq!(alarms.len(), 3);
        assert!(alarms[0].is_active);
    }
}
