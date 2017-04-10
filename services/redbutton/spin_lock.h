#pragma once
#include <sched.h>


/// Simple spin lock.
class SpinLock {
public:
    ///
    SpinLock()
        : m_lock( 0 ) {
    }

    ///
    void Lock() {
        while( !AtomicCompareAndExchange( &m_lock, 1, 0 ) )
            sched_yield();
    }

    ///
    void Unlock() {
        AtomicExchange( &m_lock, 0 );
    }

private:
    //
    volatile uint32_t m_lock;

    SpinLock( const SpinLock& ) = delete;
    SpinLock& operator =( const SpinLock& ) = delete;

    //
    bool AtomicCompareAndExchange( uint32_t volatile* dest, uint32_t xchg, uint32_t cmp ) {
        return __sync_val_compare_and_swap( dest, cmp, xchg ) == cmp;
    }

    uint32_t	AtomicExchange( uint32_t volatile* dest, uint32_t xchg ) {
        return __sync_lock_test_and_set( dest, xchg );
    }
};


//
template< typename T >
class AutoLock {
public:
    ///
    AutoLock( T& lockObject ) : m_lockObject( lockObject ) {
        m_lockObject.Lock();
    }

    ///
    ~AutoLock() {
        m_lockObject.Unlock();
    }

private:
    //
    T& m_lockObject;

    AutoLock( const AutoLock& ) = delete;
    AutoLock& operator =( const AutoLock& ) = delete;
};


//
using AutoSpinLock = AutoLock< SpinLock >;

