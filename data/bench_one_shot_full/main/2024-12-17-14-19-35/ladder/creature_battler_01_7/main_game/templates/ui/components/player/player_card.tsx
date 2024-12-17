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

let BaseCard = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ uid, ...props }, ref) => <Card ref={ref} {...props} />
)

let BaseCardHeader = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ uid, ...props }, ref) => <CardHeader ref={ref} {...props} />
)

let BaseCardContent = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ uid, ...props }, ref) => <CardContent ref={ref} {...props} />
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
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <BaseCard uid={uid} className={cn("w-[350px]", className)} {...props}>
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

PlayerCard.displayName = "PlayerCard"

PlayerCard = withClickable(PlayerCard)

export { PlayerCard }
