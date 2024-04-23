export interface FireIncident {
  id: number;
  cause_code: number;
  cause_description: string;
  discovery_datetime: string;
  containment_datetime: string;
  size_acres: number;
  size_category: number;
  year_of_fire: number;
  fips_name?: string;
  fips_code?: string;
  longitude: number;
  latitude: number;
  fire_name?: string;
  fire_code?: string;
  agency_code_id?: string;
  reporting_unit_id?: string;
}

export interface FireIncidentFilters {
  size_category?: string;
  year_of_fire_max?: number;
  year_of_fire_min?: number;
  skip?: number;
  take?: number;
}

export interface FireIncidentSearch {
  fire_incidents: FireIncident[]
  total_count: number;
}
