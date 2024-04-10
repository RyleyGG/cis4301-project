import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WildfireTypesBasedOnGeographyComponent } from './wildfire-types-based-on-geography.component';

describe('WildfireTypesBasedOnGeographyComponent', () => {
  let component: WildfireTypesBasedOnGeographyComponent;
  let fixture: ComponentFixture<WildfireTypesBasedOnGeographyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [WildfireTypesBasedOnGeographyComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(WildfireTypesBasedOnGeographyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
