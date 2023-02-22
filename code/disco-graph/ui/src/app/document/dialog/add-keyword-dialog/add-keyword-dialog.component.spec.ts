import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddKeywordDialogComponent } from './add-keyword-dialog.component';

describe('AddKeywordDialogComponent', () => {
  let component: AddKeywordDialogComponent;
  let fixture: ComponentFixture<AddKeywordDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AddKeywordDialogComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AddKeywordDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
