#include <string.h>
#include <sys/mman.h>
#include <errno.h>
#include <stdio.h>
#include <stdint.h>

#include "allocator.h"

struct Chunk
{
    uint8_t* begin;
    uint8_t* end;

    Chunk* prev;
    Chunk* next;
};
static_assert( sizeof( Chunk ) == 32, "" );

Chunk* g_freeChunksList;
const size_t SIZE = 96;// * 1024 * 1024;
uint8_t* g_memory;
uint8_t* g_memoryEnd;


//
void InitAllocator()
{
    g_memory = NULL;
    g_memory = ( uint8_t* )mmap( &g_memory, SIZE, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, 0, 0 );
    printf( "%p\n", g_memory );
    if( !g_memory ){
        printf( "mmap: %s\n", strerror( errno ) );
        return;
    }

    Chunk* chunk = ( Chunk* )g_memory;
    chunk->begin = g_memory;
    chunk->end = chunk->begin + SIZE;
    chunk->prev = nullptr;
    chunk->next = nullptr;

    g_memoryEnd = chunk->end;
    g_freeChunksList = chunk;
}


//
void* Allocate( size_t size )
{
    size += sizeof( size_t );
    //size = ( size + 31 ) & ~31;
    if( size < sizeof( Chunk ) )
        size = sizeof( Chunk );

    Chunk* chunk = g_freeChunksList;
    while( chunk )
    {
        size_t s = chunk->end - chunk->begin;
        if( s < size ){
            chunk = chunk->next;
            continue;
        }

        const bool entireChunk = ( chunk->end - chunk->begin ) == size;
        if( !entireChunk ){
            Chunk* newFreeChunk = ( Chunk* )( chunk->begin + size );

            newFreeChunk->begin = ( uint8_t* )newFreeChunk;
            newFreeChunk->end = chunk->end;

            newFreeChunk->prev = chunk->prev;
            if( chunk->prev )
                chunk->prev->next = newFreeChunk;
            else
                g_freeChunksList = newFreeChunk;

            newFreeChunk->next = chunk->next;
            if( chunk->next )
                chunk->next->prev = newFreeChunk;
        } else {
            if( chunk->prev )
                chunk->prev->next = chunk->next;
            else
                g_freeChunksList = chunk->next;

            if( chunk->next )
                chunk->next->prev = chunk->prev;
        }

        size_t* storedSize = ( size_t* )chunk;
        *storedSize = size;
        void* ptr = storedSize + 1;
        return ptr;
    }

    return nullptr;
}


//
void Free( void* ptr )
{
    void* orig_ptr = ( size_t* )ptr - 1;
    size_t size = *( size_t* )orig_ptr;
    void* end_ptr = ( uint8_t* )orig_ptr + size;

    if( !g_freeChunksList ){
        Chunk* chunk = ( Chunk* )orig_ptr;
        chunk->begin = ( uint8_t* )orig_ptr;
        chunk->end = chunk->begin + size;
        chunk->prev = nullptr;
        chunk->next = nullptr;

        g_freeChunksList = chunk;
    } else {
        Chunk* chunk = g_freeChunksList;
        Chunk* lastChunk = nullptr;
        while( chunk ){
            if( orig_ptr < chunk->begin ){
                Chunk* newChunk = ( Chunk* )orig_ptr;

                if( end_ptr == chunk->begin ){
                    Chunk safeChunk = *chunk;
                    safeChunk.begin = ( uint8_t* )orig_ptr;
                    *newChunk= safeChunk;
                } else {
                    newChunk->begin = ( uint8_t* )orig_ptr;
                    newChunk->end = newChunk->begin + size;
                    newChunk->next = chunk;
                    newChunk->prev = chunk->prev;
                    chunk->prev = newChunk;
                }

                if( newChunk->prev ){
                    Chunk* prevChunk = newChunk->prev;
                    if( prevChunk->end == newChunk->begin ){
                        prevChunk->end = newChunk->end;
                        prevChunk->next = newChunk->next;
                    } else {
                        prevChunk->next = newChunk;
                    }
                } else {
                    g_freeChunksList = newChunk;
                }

                return;
            }

            lastChunk = chunk;
            chunk = chunk->next;
        }

        //TODO check lastChunk != nullptr
        //TODO check lastChunk->next == nullptr
        //TODO check lastChunk->end <= orig_ptr
        if( lastChunk->end == orig_ptr ){
            lastChunk->end = ( uint8_t* )end_ptr;
        } else {
            Chunk* newChunk = ( Chunk* )orig_ptr;
            newChunk->begin = ( uint8_t* )orig_ptr;
            newChunk->end = newChunk->begin + size;
            newChunk->next = nullptr;
            newChunk->prev = lastChunk;
            lastChunk->next = newChunk;
        }
    }
}
