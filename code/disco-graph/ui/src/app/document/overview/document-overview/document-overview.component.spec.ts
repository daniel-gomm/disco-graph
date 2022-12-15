import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DocumentOverviewComponent } from './document-overview.component';

describe('DocumentOverviewComponent', () => {
  let component: DocumentOverviewComponent;
  let fixture: ComponentFixture<DocumentOverviewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DocumentOverviewComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DocumentOverviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
