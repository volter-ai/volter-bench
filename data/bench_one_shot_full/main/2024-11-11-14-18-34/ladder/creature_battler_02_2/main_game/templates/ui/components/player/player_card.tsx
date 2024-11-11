import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent
} from "@/components/ui/card"

interface BaseCardProps extends React.ComponentProps<typeof Card> {
  uid: string
}

interface BaseCardHeaderProps extends React.ComponentProps<typeof CardHeader> {
  uid: string
}

interface BaseCardTitleProps extends React.ComponentProps<typeof CardTitle> {
  uid: string
}

interface BaseCardContentProps extends React.ComponentProps<typeof CardContent> {
  uid: string
}

let BaseCard = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ uid, ...props }, ref) => <Card ref={ref} {...props} />
)

let BaseCardHeader = React.forwardRef<HTMLDivElement, BaseCardHeaderProps>(
  ({ uid, ...props }, ref) => <CardHeader ref={ref} {...props} />
)

let BaseCardTitle = React.forwardRef<HTMLParagraphElement, BaseCardTitleProps>(
  ({ uid, ...props }, ref) => <CardTitle ref={ref} {...props} />
)

let BaseCardContent = React.forwardRef<HTMLDivElement, BaseCardContentProps>(
  ({ uid, ...props }, ref) => <CardContent ref={ref} {...props} />
)

BaseCard = withClickable(BaseCard)
BaseCardHeader = withClickable(BaseCardHeader)
BaseCardTitle = withClickable(BaseCardTitle)
BaseCardContent = withClickable(BaseCardContent)

interface PlayerCardProps extends Omit<BaseCardProps, 'children'> {
  name: string
  imageUrl: string
}

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <BaseCard ref={ref} uid={uid} className={cn("w-[300px]", className)} {...props}>
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
