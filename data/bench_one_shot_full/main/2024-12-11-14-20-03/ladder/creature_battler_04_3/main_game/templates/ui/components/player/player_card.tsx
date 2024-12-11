import * as React from "react"
import { cn } from "@/lib/utils"
import { Card as CardPrimitive, CardContent as CardContentPrimitive, CardHeader as CardHeaderPrimitive, CardProps } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface PlayerCardProps extends CardProps {
  uid: string
  name: string
  imageUrl: string
}

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <CardPrimitive ref={ref} uid={uid} className={cn("w-[350px]", className)} {...props}>
      <CardHeaderPrimitive uid={uid}>
        <img 
          src={imageUrl}
          alt={name}
          className="w-full h-48 object-cover rounded-t-xl"
        />
      </CardHeaderPrimitive>
      <CardContentPrimitive uid={uid}>
        <h3 className="text-lg font-semibold text-center">{name}</h3>
      </CardContentPrimitive>
    </CardPrimitive>
  )
)

PlayerCard.displayName = "PlayerCard"

PlayerCard = withClickable(PlayerCard)

export { PlayerCard }
