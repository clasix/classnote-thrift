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

#import "type.h"

@protocol ClassNote <NSObject>
- (AuthResponse *) login_by_mail: (int64_t) client_id : (NSString *) client_secret : (NSString *) mail : (NSString *) password;  // throws TException
- (void) logout: (NSString *) access_token;  // throws TException
- (User *) user_get: (NSString *) access_token : (int64_t) gid;  // throws TException
- (void) user_set: (NSString *) access_token : (User *) user;  // throws TException
@end

@interface ClassNoteClient : NSObject <ClassNote> {
  id <TProtocol> inProtocol;
  id <TProtocol> outProtocol;
}
- (id) initWithProtocol: (id <TProtocol>) protocol;
- (id) initWithInProtocol: (id <TProtocol>) inProtocol outProtocol: (id <TProtocol>) outProtocol;
@end

@interface ClassNoteProcessor : NSObject <TProcessor> {
  id <ClassNote> mService;
  NSDictionary * mMethodMap;
}
- (id) initWithClassNote: (id <ClassNote>) service;
- (id<ClassNote>) service;
@end

@interface serviceConstants : NSObject {
}
@end
