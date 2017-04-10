#pragma once


//
void InitAllocator();
void* Allocate( size_t size );
void Free( void* ptr );
void PrintMap();
