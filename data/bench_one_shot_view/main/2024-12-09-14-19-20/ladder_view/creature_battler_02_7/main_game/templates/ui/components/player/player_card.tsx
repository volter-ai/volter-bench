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

BaseCard.displayName = "BaseCard"
BaseCard = withClickable(BaseCard)

interface PlayerCardProps extends BaseCardProps {
  name: string
  imageUrl: string
}

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <BaseCard uid={uid} ref={ref} className={cn("w-[350px]", className)} {...props}>
      <CardHeader>
        <CardTitle>{name}</CardTitle>
      </CardHeader>
      <CardContent>
        <img
          src={imageUrl}
          alt={name}
          className="w-full h-[200px] object-cover rounded-md"
        />
      </CardContent>
    </BaseCard>
  )
)

PlayerCard.displayName = "PlayerCard"
PlayerCard = withClickable(PlayerCard)

export { PlayerCard }
