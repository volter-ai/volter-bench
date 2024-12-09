import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

interface BaseCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

interface PlayerCardProps extends BaseCardProps {
  name: string
  imageUrl: string
}

let BaseCard = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <Card ref={ref} className={cn("w-[350px]", className)} {...props} />
  )
)

let BaseCardHeader = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardHeader ref={ref} className={className} {...props} />
  )
)

let BaseCardContent = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardContent ref={ref} className={className} {...props} />
  )
)

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <BaseCard ref={ref} uid={uid} className={cn("w-[350px]", className)} {...props}>
      <BaseCardHeader uid={uid}>
        <CardTitle>{name}</CardTitle>
      </BaseCardHeader>
      <BaseCardContent uid={uid}>
        <img
          src={imageUrl}
          alt={name}
          className="w-full h-[200px] object-cover rounded-md"
        />
      </BaseCardContent>
    </BaseCard>
  )
)

BaseCard.displayName = "BaseCard"
BaseCardHeader.displayName = "BaseCardHeader"
BaseCardContent.displayName = "BaseCardContent"
PlayerCard.displayName = "PlayerCard"

BaseCard = withClickable(BaseCard)
BaseCardHeader = withClickable(BaseCardHeader)
BaseCardContent = withClickable(BaseCardContent)
PlayerCard = withClickable(PlayerCard)

export { PlayerCard }
