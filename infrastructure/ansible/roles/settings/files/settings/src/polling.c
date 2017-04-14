#ifndef _polling_c_
#define _polling_c_

#include <sys/epoll.h>

#define queue_size 1024

struct {
  size_t size;
  size_t current;
  struct epoll_event events[queue_size];
} epoll_queue;

int efd;

int initPoll() {
	return efd = epoll_create1(0);
}

int addListener(int fd, uint32_t events) {
	struct epoll_event event;

	event.data.fd = fd;
	event.events = events;
	return epoll_ctl(efd, EPOLL_CTL_ADD, fd, &event);
}

int addRead(int fd) {
	return addListener(fd, EPOLLIN);
}

int addWrite(int fd) {
	return addListener(fd, EPOLLOUT);
}

int removeListener(int fd, uint32_t events) {
	struct epoll_event event;

	event.data.fd = fd;
	event.events = events;
	return epoll_ctl(efd, EPOLL_CTL_DEL, fd, &event);
}

int removeRead(int fd) {
	return removeListener(fd, EPOLLIN);
}

int removeWrite(int fd) {
	return removeListener(fd, EPOLLOUT);
}

void getEvent(int* fd, int* event) {
	while (epoll_queue.current >= epoll_queue.size) {
		epoll_queue.size = epoll_wait(efd, epoll_queue.events, queue_size, -1);
		epoll_queue.current = 0;
	}

	*fd = epoll_queue.events[epoll_queue.current].data.fd;
	*event = epoll_queue.events[epoll_queue.current].events;
	++epoll_queue.current;
}

#undef queue_size

#endif
