import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card,
  CardHeader,
  CardContent,
  CardFooter,
  CardTitle,
} from "@/components/ui/card"

interface BaseCardProps extends React.ComponentProps<typeof Card> {
  uid: string
}

interface PlayerCardProps extends BaseCardProps {
  name: string
  imageUrl: string
}

let BaseCard = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <Card ref={ref} className={className} {...props} />
  )
)

let BaseCardHeader = React.forwardRef<
  HTMLDivElement,
  BaseCardProps & React.ComponentProps<typeof CardHeader>
>(({ uid, ...props }, ref) => <CardHeader ref={ref} {...props} />)

let BaseCardContent = React.forwardRef<
  HTMLDivElement,
  BaseCardProps & React.ComponentProps<typeof CardContent>
>(({ uid, ...props }, ref) => <CardContent ref={ref} {...props} />)

let BaseCardFooter = React.forwardRef<
  HTMLDivElement,
  BaseCardProps & React.ComponentProps<typeof CardFooter>
>(({ uid, ...props }, ref) => <CardFooter ref={ref} {...props} />)

let BaseCardTitle = React.forwardRef<
  HTMLParagraphElement,
  BaseCardProps & React.ComponentProps<typeof CardTitle>
>(({ uid, ...props }, ref) => <CardTitle ref={ref} {...props} />)

BaseCard = withClickable(BaseCard)
BaseCardHeader = withClickable(BaseCardHeader)
BaseCardContent = withClickable(BaseCardContent)
BaseCardFooter = withClickable(BaseCardFooter)
BaseCardTitle = withClickable(BaseCardTitle)

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <BaseCard ref={ref} className={cn("w-[350px]", className)} uid={uid} {...props}>
      <BaseCardHeader uid={uid}>
        <BaseCardTitle uid={uid}>{name}</BaseCardTitle>
      </BaseCardHeader>
      <BaseCardContent uid={uid}>
        <img
          src={imageUrl}
          alt={name}
          className="w-full h-[200px] object-cover rounded-md"
        />
      </BaseCardContent>
      <BaseCardFooter uid={uid} className="flex justify-between" />
    </BaseCard>
  )
)

PlayerCard.displayName = "PlayerCard"

PlayerCard = withClickable(PlayerCard)

export { PlayerCard }
