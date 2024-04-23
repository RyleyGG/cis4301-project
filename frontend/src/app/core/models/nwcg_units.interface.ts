export interface NWCGUnit {
  unit_id: string;
  parent_agency: string;
  agency_name: string;
  department_or_state?: string;
  wildland_role: string;
  geographic_area_code: string;
  unit_name: string;
  unit_type: string;
  unit_code: string;
  state_affiliation: string;
  country: string;
}

export interface NWCGUnitFilters {
  agency_name?: string;
  wildland_role?: string;
  geographic_area_code?: string;
  skip?: number;
  take?: number;
}

export interface NWCGUnitSearch {
  nwcg_units: NWCGUnit[]
  total_count: number;
}
