import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SizeOfWildfireTypesComponent } from './size-of-wildfire-types.component';

describe('SizeOfWildfireTypesComponent', () => {
  let component: SizeOfWildfireTypesComponent;
  let fixture: ComponentFixture<SizeOfWildfireTypesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SizeOfWildfireTypesComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(SizeOfWildfireTypesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
