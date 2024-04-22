// WildFire Sizes Based on Geographical Area

export interface wildfireSizeBasedOnGeoFilters {
  start_date: Date;
  end_date: Date;
  geographic_area: string;
}

// TODO: define return structure for graph
export interface wildfireSizeBasedOnGeoData {

}

// WildFire Types based on Geographical Area

export interface WildfireTypesBasedOnGeoFilters{
  start_date: Date;  // Date property for calendar binding
  end_date: Date;  // Date property for calendar binding
  geographic_area: string;
  wildfire_type: string;
}

export interface WildfireTypesBasedOnGeoData{

}


// Agency Containment Time 
export interface AgencyContaintmentTimeFilters{
  start_date: Date;  // Date property for calendar binding
  end_date: Date;  // Date property for calendar binding
  reporting_agency: string;
}

export interface AgencyContaintmentTimeData{

}


// Size of Wildfire Types
export interface SizeOfWildfireTypesFilters{
  start_date: Date;  // Date property for calendar binding
  end_date: Date;  // Date property for calendar binding
  reporting_agency: string;
  wildfire_type: string;
}

export interface SizeOfWildfireTypesData{

}

// WildFire Size and Frequency
export interface WildFireChangesInSizeAndFrequencyFilters{
  start_date: Date;  // Date property for calendar binding
  end_date: Date;  // Date property for calendar binding
}

export interface WildFireChangesInSizeAndFrequencyData{

}
