import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface PlayerCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
}

let BaseCard = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement> & {uid: string}>(
  ({ className, uid, ...props }, ref) => (
    <Card ref={ref} className={className} {...props} />
  )
)

let BaseCardHeader = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement> & {uid: string}>(
  ({ className, uid, ...props }, ref) => (
    <CardHeader ref={ref} className={className} {...props} />
  )
)

let BaseCardContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement> & {uid: string}>(
  ({ className, uid, ...props }, ref) => (
    <CardContent ref={ref} className={className} {...props} />
  )
)

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <BaseCard uid={`${uid}-card`} className={cn("w-[350px]", className)} {...props} ref={ref}>
      <BaseCardHeader uid={`${uid}-header`}>
        <img 
          src={imageUrl}
          alt={name}
          className="w-full h-48 object-cover rounded-t-xl"
        />
      </BaseCardHeader>
      <BaseCardContent uid={`${uid}-content`}>
        <h3 className="text-lg font-semibold text-center">{name}</h3>
      </BaseCardContent>
    </BaseCard>
  )
)

BaseCard = withClickable(BaseCard)
BaseCardHeader = withClickable(BaseCardHeader)
BaseCardContent = withClickable(BaseCardContent)
PlayerCard = withClickable(PlayerCard)

BaseCard.displayName = "BaseCard"
BaseCardHeader.displayName = "BaseCardHeader" 
BaseCardContent.displayName = "BaseCardContent"
PlayerCard.displayName = "PlayerCard"

export { PlayerCard }
