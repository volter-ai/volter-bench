import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

let BaseCard = React.forwardRef<HTMLDivElement, React.ComponentProps<typeof Card> & { uid: string }>(
  ({ uid, ...props }, ref) => <Card ref={ref} {...props} />
)

let BaseCardHeader = React.forwardRef<HTMLDivElement, React.ComponentProps<typeof CardHeader> & { uid: string }>(
  ({ uid, ...props }, ref) => <CardHeader ref={ref} {...props} />
)

let BaseCardContent = React.forwardRef<HTMLDivElement, React.ComponentProps<typeof CardContent> & { uid: string }>(
  ({ uid, ...props }, ref) => <CardContent ref={ref} {...props} />
)

let BaseCardTitle = React.forwardRef<HTMLParagraphElement, React.ComponentProps<typeof CardTitle> & { uid: string }>(
  ({ uid, ...props }, ref) => <CardTitle ref={ref} {...props} />
)

BaseCard = withClickable(BaseCard)
BaseCardHeader = withClickable(BaseCardHeader)
BaseCardContent = withClickable(BaseCardContent)
BaseCardTitle = withClickable(BaseCardTitle)

interface PlayerCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
}

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <BaseCard uid={uid} ref={ref} className={cn("w-[300px]", className)} {...props}>
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
