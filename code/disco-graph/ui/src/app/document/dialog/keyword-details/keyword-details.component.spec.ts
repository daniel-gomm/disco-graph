import { ComponentFixture, TestBed } from '@angular/core/testing';

import { KeywordDetailsComponent } from './keyword-details.component';

describe('KeywordDetailsComponent', () => {
  let component: KeywordDetailsComponent;
  let fixture: ComponentFixture<KeywordDetailsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ KeywordDetailsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(KeywordDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
