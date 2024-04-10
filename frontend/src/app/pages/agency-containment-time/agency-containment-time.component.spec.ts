import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AgencyContainmentTimeComponent } from './agency-containment-time.component';

describe('AgencyContainmentTimeComponent', () => {
  let component: AgencyContainmentTimeComponent;
  let fixture: ComponentFixture<AgencyContainmentTimeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AgencyContainmentTimeComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(AgencyContainmentTimeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
