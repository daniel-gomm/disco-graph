import { ComponentFixture, TestBed } from '@angular/core/testing';

import { YearsFilterComponent } from './years-filter.component';

describe('YearsFilterComponent', () => {
  let component: YearsFilterComponent;
  let fixture: ComponentFixture<YearsFilterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ YearsFilterComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(YearsFilterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
