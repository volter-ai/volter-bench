import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface BaseCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

let BaseCard = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <Card ref={ref} uid={uid} className={cn("", className)} {...props} />
  )
)

let BaseCardHeader = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardHeader ref={ref} uid={uid} className={cn("", className)} {...props} />
  )
)

let BaseCardContent = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardContent ref={ref} uid={uid} className={cn("", className)} {...props} />
  )
)

BaseCard = withClickable(BaseCard)
BaseCardHeader = withClickable(BaseCardHeader)
BaseCardContent = withClickable(BaseCardContent)

interface PlayerCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
}

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => {
    return (
      <BaseCard ref={ref} uid={uid} className={cn("w-[300px]", className)} {...props}>
        <BaseCardHeader uid={uid}>
          <img
            src={imageUrl}
            alt={name}
            className="w-full h-48 object-cover rounded-t-xl"
          />
        </BaseCardHeader>
        <BaseCardContent uid={uid}>
          <h3 className="text-lg font-bold text-center">{name}</h3>
        </BaseCardContent>
      </BaseCard>
    )
  }
)

PlayerCard.displayName = "PlayerCard"

PlayerCard = withClickable(PlayerCard)

export { PlayerCard }
