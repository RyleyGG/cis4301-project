export interface ReportingAgency {
  agency_code: string;
  agency_name?: string;
  reporting_unit_id: string;
  reporting_unit_name: string;
}

export interface ReportingAgencyFilters {
  agency_code?: string;
  reporting_unit_id?: string;
  reporting_unit_name?: string;
  skip?: number;
  take?: number;
}

export interface ReportingAgencySearch {
  reporting_agencies: ReportingAgency[]
  total_count: number;
}
