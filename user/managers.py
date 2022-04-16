from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):

  # Create and save a User
  def create_user(self, username, phone_number, nid_number, atm_card, password=None):

    if not username:
      raise ValueError('The Username must be set')
    if not phone_number:
      raise ValueError('Users must have a Phone Number')
    if not nid_number:
      raise ValueError('Users must have a NID Number')
    if not atm_card:
      raise ValueError('Users must have a ATM Card')
        
    user = self.model(
      username      = username,
      phone_number  = phone_number,
      nid_number    = nid_number,
      atm_card      = atm_card,
    )
    user.set_password(password)
    
    user.save(using=self._db)
    return user

  # Create and save a SuperUser
  def create_superuser(self, username, phone_number, nid_number, atm_card, password):

    user = self.create_user(
      username      = username,
      password      = password,
      phone_number  = phone_number,
      nid_number    = nid_number,
      atm_card      = atm_card,
    )

    user.is_admin     = True
    user.is_staff     = True
    user.is_superuser = True

    user.save(using=self._db)
    return user