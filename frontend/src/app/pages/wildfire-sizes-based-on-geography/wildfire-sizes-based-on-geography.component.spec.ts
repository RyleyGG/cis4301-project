import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WildfireSizesBasedOnGeographyComponent } from './wildfire-sizes-based-on-geography.component';

describe('WildfireSizesBasedOnGeographyComponent', () => {
  let component: WildfireSizesBasedOnGeographyComponent;
  let fixture: ComponentFixture<WildfireSizesBasedOnGeographyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [WildfireSizesBasedOnGeographyComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(WildfireSizesBasedOnGeographyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
