// WildFire Size and Frequency
export interface WildFireChangesInSizeAndFrequencyFilters {
  start_date?: number;
  end_date?: number;
}

export interface WildFireChangesInSizeAndFrequency {
  year_of_fire: number;
  avg_fire_size: number;
  total_number_of_fires: number
  total_fires_size: number
}

// WildFire Types based on Geographical Area

export interface WildfireTypesBasedOnGeoFilters {
  start_date?: number;
  end_date?: number;
  geographic_area?: string[];
  cause_description?: string[];
}

export interface UnitInformation {
  unit_name: string;
  geographic_area_code: string;
}

export interface AgencyInformation {
  agency_name: string;
  agency_code: string;
}

export interface WildfireTypesBasedOnGeoData {
  year_of_fire: number;
  cause_description?: string;
  geographic_area_code?: string;
  avg_fire_size: number;
  total_number_of_fires: number;
  total_fires_size: number;
  cause_description_count: number;
}


// Agency Containment Time
export interface AgencyContainmentTimeFilters {
  start_date?: number;
  end_date?: number;
  reporting_agencies?: string[];
}

export interface AgencyContainmentTimeData {
  year_of_fire: number;
  reporting_unit_name?: string;
  time_to_contain: number;
  total_fires: number;
  avg_size_of_fires: number;
}

// Size of Wildfire Types
export interface SizeOfWildfireTypesFilters {
  start_date?: Date;
  end_date?: Date;
  reporting_agency?: string;
  wildfire_type?: string;
}

export interface SizeOfWildfireTypesData {
  year_of_fire?: number;
  reporting_unit_name?: string;
  fires?: number;
  avg_fire_size?: number;
  largest_fire_size?: number;
}


// WildFire Sizes Based on Geographical Area

export interface wildfireSizeBasedOnGeoFilters {
  start_date?: Date;
  end_date?: Date;
  geographic_area?: string;
}

// TODO: define return structure for graph
export interface wildfireSizeBasedOnGeoData {
  year_of_fire?: number;
  state_affiliation?: string;
  avg_fire_size?: number;
  largest_fire_size?: number;
}








