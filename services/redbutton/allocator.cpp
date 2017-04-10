#include <string.h>
#include <sys/mman.h>
#include <errno.h>
#include <stdio.h>
#include <stdint.h>
#include "spin_lock.h"
#include "allocator.h"

#if 0
    #define DEBUG 1
#endif

struct Chunk
{
    uint8_t* end;

    Chunk* prev;
    Chunk* next;
};

Chunk* g_freeChunksList;
Chunk* g_curChunk;
const size_t SIZE = 16 * 1024 * 1024;
uint8_t* g_memory;
uint8_t* g_memoryEnd;

//
SpinLock g_lock;


//
void InitAllocator()
{
    g_memory = NULL;
    g_memory = ( uint8_t* )mmap( &g_memory, SIZE, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, 0, 0 );
    if( !g_memory ){
        printf( "mmap: %s\n", strerror( errno ) );
        return;
    }

    Chunk* chunk = ( Chunk* )g_memory;
    chunk->end = ( uint8_t* )chunk + SIZE;
    chunk->prev = nullptr;
    chunk->next = nullptr;

    g_memoryEnd = chunk->end;
    g_freeChunksList = chunk;
    g_curChunk = chunk;

#if DEBUG
    printf( "%p : %p\n", g_memory, g_memoryEnd );
#endif
}


//
void* AllocateUnsafe( size_t size )
{
    size += sizeof( Chunk );

    Chunk* chunk = g_curChunk;
    while( chunk )
    {
        uint8_t* chkBegin = ( uint8_t* )chunk;
        size_t s = chunk->end - chkBegin;
        if( s < size ){
            chunk = chunk->next;
            continue;
        }

        const bool entireChunk = ( chunk->end - chkBegin ) == size;
        if( !entireChunk ){
            Chunk* newFreeChunk = ( Chunk* )( chkBegin + size );

            *newFreeChunk = *chunk;

            if( newFreeChunk->prev )
                newFreeChunk->prev->next = newFreeChunk;
            else
                g_freeChunksList = newFreeChunk;

            if( newFreeChunk->next )
                newFreeChunk->next->prev = newFreeChunk;

            g_curChunk = newFreeChunk;
        } else {
            g_curChunk = nullptr;

            if( chunk->prev ){
                chunk->prev->next = chunk->next;
                g_curChunk = chunk->prev;
            }
            else
                g_freeChunksList = chunk->next;

            if( chunk->next ){
                chunk->next->prev = chunk->prev;
                g_curChunk = chunk->next;
            }
        }

        uint8_t* ptr = chkBegin;
        ptr += sizeof( Chunk );

        size_t* storedSize = ( size_t* )ptr - 1;
        *storedSize = size;
        return ptr;
    }

    return nullptr;
}


//
void Merge()
{
#ifdef DEBUG
    printf( "Merge\n" );
#endif

    Chunk* chunk = g_freeChunksList;
    while( chunk ){
        Chunk* nextChunk = chunk->next;
        if( !nextChunk )
            break;

        if( chunk->end != ( uint8_t* )nextChunk ){
            chunk = nextChunk;
            continue;
        }

        chunk->end = nextChunk->end;
        chunk->next = nextChunk->next;
        if( chunk->next )
            chunk->next->prev = chunk;
    }

    g_curChunk = g_freeChunksList;
#ifdef DEBUG
    PrintMap();
#endif
}


//
void* Allocate( size_t size )
{
    AutoSpinLock autoLock( g_lock );
#if DEBUG
    printf( "Allocate %u %u\n", size, size + sizeof( Chunk ) );
#endif

    void* ptr = AllocateUnsafe( size );
    if( !ptr ){
        Merge();
        ptr = AllocateUnsafe( size );
    }

#ifdef DEBUG
    printf( "\t%p\n", ptr );
    PrintMap();
#endif
    return ptr;
}


//
void Free( void* ptr )
{
    AutoSpinLock autoLock( g_lock );
#ifdef DEBUG
    printf( "Free %p\n", ptr );
#endif
    if( !ptr )
        return;

    void* orig_ptr = ( Chunk* )ptr - 1;
    size_t size = *( ( size_t* )ptr - 1 );

    if( !g_freeChunksList ){
        Chunk* chunk = ( Chunk* )orig_ptr;
        chunk->end = ( uint8_t* )chunk + size;
        chunk->prev = nullptr;
        chunk->next = nullptr;

        g_freeChunksList = chunk;
        g_curChunk = chunk;
    } else {
        Chunk* chunk = g_freeChunksList;
        Chunk* lastChunk = nullptr;
        while( chunk ){
            if( orig_ptr < chunk ){
                Chunk* newChunk = ( Chunk* )orig_ptr;

                newChunk->end = ( uint8_t* )newChunk + size;
                newChunk->next = chunk;
                newChunk->prev = chunk->prev;
                chunk->prev = newChunk;

                if( newChunk->prev )
                    newChunk->prev->next = newChunk;
                else
                    g_freeChunksList = newChunk;
#ifdef DEBUG
    PrintMap();
#endif

                return;
            }

            lastChunk = chunk;
            chunk = chunk->next;
        }

        //TODO check lastChunk != nullptr
        //TODO check lastChunk->next == nullptr
        //TODO check lastChunk->end <= orig_ptr
        {
            Chunk* newChunk = ( Chunk* )orig_ptr;
            newChunk->end = ( uint8_t* )newChunk + size;
            newChunk->next = nullptr;
            newChunk->prev = lastChunk;
            lastChunk->next = newChunk;
        }
    }
#ifdef DEBUG
    PrintMap();
#endif
}


//
void PrintMap()
{
    printf( "Start: %p\n", g_freeChunksList );
    printf( "Curr : %p\n", g_curChunk );
    Chunk* chunk = g_freeChunksList;
    while( chunk ){
        printf( "%p %p %p %p %u\n", chunk, chunk->end, chunk->prev, chunk->next, chunk->end - ( uint8_t* )chunk );
        chunk = chunk->next;
    }
}
