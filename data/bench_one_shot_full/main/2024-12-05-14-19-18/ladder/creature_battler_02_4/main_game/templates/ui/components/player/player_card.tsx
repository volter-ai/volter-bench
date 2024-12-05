import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card,
  CardHeader,
  CardContent,
  CardFooter,
  CardTitle,
  CardDescription,
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
    <Card ref={ref} className={cn("w-[350px]", className)} {...props} />
  )
)

let BaseCardHeader = React.forwardRef<
  HTMLDivElement,
  React.ComponentProps<typeof CardHeader> & { uid: string }
>(({ uid, ...props }, ref) => <CardHeader ref={ref} {...props} />)

let BaseCardContent = React.forwardRef<
  HTMLDivElement,
  React.ComponentProps<typeof CardContent> & { uid: string }
>(({ uid, ...props }, ref) => <CardContent ref={ref} {...props} />)

let BaseCardTitle = React.forwardRef<
  HTMLParagraphElement,
  React.ComponentProps<typeof CardTitle> & { uid: string }
>(({ uid, ...props }, ref) => <CardTitle ref={ref} {...props} />)

BaseCard.displayName = "BaseCard"
BaseCardHeader.displayName = "BaseCardHeader"
BaseCardContent.displayName = "BaseCardContent"
BaseCardTitle.displayName = "BaseCardTitle"

BaseCard = withClickable(BaseCard)
BaseCardHeader = withClickable(BaseCardHeader)
BaseCardContent = withClickable(BaseCardContent)
BaseCardTitle = withClickable(BaseCardTitle)

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <BaseCard ref={ref} uid={uid} className={cn("w-[350px]", className)} {...props}>
      <BaseCardHeader uid={`${uid}-header`}>
        <BaseCardTitle uid={`${uid}-title`}>{name}</BaseCardTitle>
      </BaseCardHeader>
      <BaseCardContent uid={`${uid}-content`}>
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
