import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WildfiresChangesComponent } from './wildfires-changes.component';

describe('WildfiresChangesComponent', () => {
  let component: WildfiresChangesComponent;
  let fixture: ComponentFixture<WildfiresChangesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [WildfiresChangesComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(WildfiresChangesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
