import { ComponentFixture, TestBed } from '@angular/core/testing';

import { KeywordSuggestionComponent } from './keyword-suggestion.component';

describe('KeywordSuggestionComponent', () => {
  let component: KeywordSuggestionComponent;
  let fixture: ComponentFixture<KeywordSuggestionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ KeywordSuggestionComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(KeywordSuggestionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
