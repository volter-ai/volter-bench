import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

let PlayerCardBase = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <Card ref={ref} className={cn("w-[300px]", className)} {...props} />
  )
)

let PlayerCardHeader = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <CardHeader ref={ref} className={className} {...props} />
  )
)

let PlayerCardTitle = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLHeadingElement>>(
  ({ className, ...props }, ref) => (
    <CardTitle ref={ref} className={className} {...props} />
  )
)

let PlayerCardContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <CardContent ref={ref} className={className} {...props} />
  )
)

PlayerCardBase.displayName = "PlayerCardBase"
PlayerCardHeader.displayName = "PlayerCardHeader"
PlayerCardTitle.displayName = "PlayerCardTitle"
PlayerCardContent.displayName = "PlayerCardContent"

PlayerCardBase = withClickable(PlayerCardBase)
PlayerCardHeader = withClickable(PlayerCardHeader)
PlayerCardTitle = withClickable(PlayerCardTitle)
PlayerCardContent = withClickable(PlayerCardContent)

interface PlayerCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
}

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <PlayerCardBase uid={uid} className={cn("w-[300px]", className)} {...props} ref={ref}>
      <PlayerCardHeader uid={uid}>
        <PlayerCardTitle uid={uid}>{name}</PlayerCardTitle>
      </PlayerCardHeader>
      <PlayerCardContent uid={uid}>
        <img
          src={imageUrl}
          alt={name}
          className="w-full h-[200px] object-cover rounded-md"
        />
      </PlayerCardContent>
    </PlayerCardBase>
  )
)

PlayerCard.displayName = "PlayerCard"

PlayerCard = withClickable(PlayerCard)

export { PlayerCard }
