import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DocumentTabComponent } from './document-tab.component';

describe('DocumentTabComponent', () => {
  let component: DocumentTabComponent;
  let fixture: ComponentFixture<DocumentTabComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DocumentTabComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DocumentTabComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
