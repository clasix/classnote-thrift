/**
 * Autogenerated by Thrift Compiler (0.8.0)
 *
 * DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
 *  @generated
 */

#import <Foundation/Foundation.h>

#import <TProtocol.h>
#import <TApplicationException.h>
#import <TProtocolUtil.h>
#import <TProcessor.h>


enum ExceptionCode {
  ExceptionCode_PERMISSION_DENIED = 101,
  ExceptionCode_INNER_ERROR = 102
};

@interface Exception : NSException <NSCoding> {
  int __code;
  NSString * __message;

  BOOL __code_isset;
  BOOL __message_isset;
}

#if TARGET_OS_IPHONE || (MAC_OS_X_VERSION_MAX_ALLOWED >= MAC_OS_X_VERSION_10_5)
@property (nonatomic, getter=code, setter=setCode:) int code;
@property (nonatomic, retain, getter=message, setter=setMessage:) NSString * message;
#endif

- (id) initWithCode: (int) code message: (NSString *) message;

- (void) read: (id <TProtocol>) inProtocol;
- (void) write: (id <TProtocol>) outProtocol;

- (int) code;
- (void) setCode: (int) code;
- (BOOL) codeIsSet;

- (NSString *) message;
- (void) setMessage: (NSString *) message;
- (BOOL) messageIsSet;

@end

@interface exceptionConstants : NSObject {
}
@end
