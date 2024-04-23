// WildFire Sizes Based on Geographical Area

export interface wildfireSizeBasedOnGeoFilters {
  start_date?: Date;
  end_date?: Date;
  geographic_area?: string;
}

// TODO: define return structure for graph
export interface wildfireSizeBasedOnGeoData {

}

// WildFire Types based on Geographical Area

export interface WildfireTypesBasedOnGeoFilters{
  start_date?: Date;
  end_date?: Date;
  geographic_area?: string;
  wildfire_type?: string;
}

export interface WildfireTypesBasedOnGeoData{

}


// Agency Containment Time 
export interface AgencyContaintmentTimeFilters{
  start_date?: Date;
  end_date?: Date;
  reporting_agency?: string;
}

export interface AgencyContaintmentTimeData{

}


// Size of Wildfire Types
export interface SizeOfWildfireTypesFilters{
  start_date?: Date;
  end_date?: Date;
  reporting_agency?: string;
  wildfire_type?: string;
}

export interface SizeOfWildfireTypesData{

}


// WildFire Size and Frequency
export interface WildFireChangesInSizeAndFrequency{
  year_of_fire?: number;
  avg_fire_size?: number;
  total_number_of_fires?: number
  total_fires_size?: number
}


export interface WildFireChangesInSizeAndFrequencyFilters{
  start_date?: Date;
  end_date?: Date;
}


