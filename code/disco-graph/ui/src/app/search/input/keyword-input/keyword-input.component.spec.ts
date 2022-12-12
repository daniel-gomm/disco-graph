import { ComponentFixture, TestBed } from '@angular/core/testing';

import { KeywordInputComponent } from './keyword-input.component';

describe('KeywordInputComponent', () => {
  let component: KeywordInputComponent;
  let fixture: ComponentFixture<KeywordInputComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ KeywordInputComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(KeywordInputComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
