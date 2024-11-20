import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface PlayerCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
}

interface PlayerCardHeaderProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  imageUrl: string
  alt: string
}

interface PlayerCardContentProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
}

let PlayerCardHeader = React.forwardRef<HTMLDivElement, PlayerCardHeaderProps>(
  ({ className, uid, imageUrl, alt, ...props }, ref) => (
    <CardHeader uid={uid} ref={ref} className={className} {...props}>
      <img 
        src={imageUrl}
        alt={alt}
        className="w-full h-48 object-cover rounded-t-xl"
      />
    </CardHeader>
  )
)

let PlayerCardContent = React.forwardRef<HTMLDivElement, PlayerCardContentProps>(
  ({ className, uid, name, ...props }, ref) => (
    <CardContent uid={uid} ref={ref} className={className} {...props}>
      <h3 className="text-lg font-bold text-center">{name}</h3>
    </CardContent>
  )
)

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <Card uid={uid} ref={ref} className={cn("w-[300px]", className)} {...props}>
      <PlayerCardHeader uid={uid} imageUrl={imageUrl} alt={name} />
      <PlayerCardContent uid={uid} name={name} />
    </Card>
  )
)

PlayerCard.displayName = "PlayerCard"
PlayerCardHeader.displayName = "PlayerCardHeader"
PlayerCardContent.displayName = "PlayerCardContent"

PlayerCard = withClickable(PlayerCard)
PlayerCardHeader = withClickable(PlayerCardHeader)
PlayerCardContent = withClickable(PlayerCardContent)

export { PlayerCard, PlayerCardHeader, PlayerCardContent }
