import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DocumentComponent } from './components/document/document.component';
import { SearchComponent } from './components/search/search.component';
import { PageNotFoundComponent } from './components/util/page-not-found/page-not-found.component';

const routes: Routes = [
  {path: 'search', component: SearchComponent},
  {path: 'document', component: DocumentComponent},
  {path: '', redirectTo: '/search', pathMatch: 'full'},
  {path: '**', component: PageNotFoundComponent}
]

@NgModule({
  imports: [RouterModule.forRoot(routes,
    {enableTracing: true})], // TODO: Use only for debugging
  exports: [RouterModule]
})
export class AppRoutingModule { }
